import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Primordial Visualizador", layout="wide")

def main():
    st.title("Primordial - Visualizador Pro")
    st.write("Sube la foto de tu espacio y personalízalo con nuestros cojines.")

    # El código HTML/React que ya tienes, adaptado para Streamlit
    react_code = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .cushion-item { touch-action: none; user-select: none; }
            .resize-handle { 
                width: 24px; height: 24px; background: white; border: 3px solid black; 
                border-radius: 50%; position: absolute; bottom: -12px; right: -12px; 
                cursor: nwse-resize; z-index: 50; box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .delete-btn {
                width: 24px; height: 24px; background: #ef4444; color: white; 
                border-radius: 50%; position: absolute; top: -12px; right: -12px; 
                display: flex; align-items: center; justify-content: center;
                font-weight: bold; font-size: 14px; cursor: pointer; z-index: 60;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3); border: 2px solid white;
            }
        </style>
    </head>
    <body class="bg-stone-50">
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect } = React;
            
            const CUSHION_CATALOG = [
                { id: 'c1', name: 'Ajedrez Terciopelo', src: 'https://i.postimg.cc/Cz2Nqz5R/image.png' },
                { id: 'c2', name: 'Cojín 2', src: 'https://i.postimg.cc/R3dJwDdd/image.png' },
                { id: 'c3', name: 'Cojín 3', src: 'https://i.postimg.cc/SnNhJ1nt/image.png' },
                { id: 'c4', name: 'Cojín 4', src: 'https://i.postimg.cc/878ZY7GD/image.png' }
            ];

            function App() {
                const [bgImage, setBgImage] = useState(null);
                const [placedItems, setPlacedItems] = useState([]);
                const [selectedId, setSelectedId] = useState(null);
                const [action, setAction] = useState(null);

                const handleImageUpload = (e) => {
                    const file = e.target.files[0];
                    if (file) setBgImage(URL.createObjectURL(file));
                };

                const addCushion = (c) => {
                    if(!bgImage) return alert("Primero sube una foto de tu sala");
                    const newItem = { id: Date.now(), src: c.src, x: 150, y: 150, w: 180 };
                    setPlacedItems([...placedItems, newItem]);
                    setSelectedId(newItem.id);
                };

                const deleteItem = (id, e) => {
                    e.stopPropagation();
                    setPlacedItems(prev => prev.filter(item => item.id !== id));
                    setSelectedId(null);
                };

                const onStart = (e, id, type) => {
                    e.stopPropagation();
                    setSelectedId(id);
                    const item = placedItems.find(i => i.id === id);
                    const clientX = e.clientX || e.touches?.[0].clientX;
                    const clientY = e.clientY || e.touches?.[0].clientY;
                    
                    setAction({ 
                        id, type, startX: clientX, startY: clientY, 
                        initX: item.x, initY: item.y, initW: item.w 
                    });
                };

                useEffect(() => {
                    const onMove = (e) => {
                        if (!action) return;
                        const clientX = e.clientX || e.touches?.[0].clientX;
                        const clientY = e.clientY || e.touches?.[0].clientY;
                        const deltaX = clientX - action.startX;
                        const deltaY = clientY - action.startY;

                        setPlacedItems(prev => prev.map(item => {
                            if (item.id !== action.id) return item;
                            if (action.type === 'move') {
                                return { ...item, x: action.initX + deltaX, y: action.initY + deltaY };
                            } else {
                                return { ...item, w: Math.max(40, action.initW + deltaX) };
                            }
                        }));
                    };
                    const onEnd = () => setAction(null);
                    window.addEventListener('pointermove', onMove);
                    window.addEventListener('pointerup', onEnd);
                    return () => {
                        window.removeEventListener('pointermove', onMove);
                        window.removeEventListener('pointerup', onEnd);
                    };
                }, [action]);

                return (
                    <div className="min-h-screen flex flex-col font-sans select-none overflow-hidden">
                        <main className="flex flex-col lg:flex-row flex-1">
                            <aside className="w-full lg:w-64 bg-white p-4 border-r space-y-6 z-10">
                                <div>
                                    <h2 className="text-[10px] font-black uppercase text-stone-500 mb-2">1. Carga tu espacio</h2>
                                    <input type="file" onChange={handleImageUpload} className="text-xs w-full" />
                                </div>
                                <hr />
                                <div>
                                    <h2 className="text-[10px] font-black uppercase text-stone-500 mb-4">2. Cojines</h2>
                                    <div className="grid grid-cols-2 gap-2">
                                        {CUSHION_CATALOG.map(c => (
                                            <div key={c.id} onClick={() => addCushion(c)} className="group border rounded-lg p-1 hover:border-black cursor-pointer bg-stone-50">
                                                <img src={c.src} className="w-full h-12 object-contain mb-1" />
                                                <p className="text-[8px] text-center uppercase font-bold">{c.name}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </aside>

                            <section className="flex-1 p-4 flex items-start justify-center bg-stone-100 relative min-h-[600px]" onPointerDown={() => setSelectedId(null)}>
                                {!bgImage ? (
                                    <p className="mt-20 text-stone-400 italic text-center">Sube una foto para empezar</p>
                                ) : (
                                    <div className="relative shadow-xl bg-white border-4 border-white inline-block">
                                        <img src={bgImage} className="max-h-[80vh] block pointer-events-none" />
                                        {placedItems.map(item => (
                                            <div 
                                                key={item.id} 
                                                onPointerDown={(e) => onStart(e, item.id, 'move')}
                                                style={{ left: item.x, top: item.y, width: item.w, transform: 'translate(-50%, -50%)' }} 
                                                className={`absolute cushion-item ${selectedId === item.id ? 'ring-2 ring-black ring-offset-2' : ''}`}
                                            >
                                                <img src={item.src} className="w-full h-full object-contain drop-shadow-xl pointer-events-none" />
                                                {selectedId === item.id && (
                                                    <>
                                                        <div className="delete-btn" onPointerDown={(e) => deleteItem(item.id, e)}>✕</div>
                                                        <div className="resize-handle" onPointerDown={(e) => onStart(e, item.id, 'resize')} />
                                                    </>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </section>
                        </main>
                    </div>
                );
            }

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<App />);
        </script>
    </body>
    </html>
    """

    # Renderizar el componente
    components.html(react_code, height=800, scrolling=True)

if __name__ == "__main__":
    main()