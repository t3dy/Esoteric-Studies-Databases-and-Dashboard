import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Search, Loader } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

interface AlchemyImage {
    id: number;
    image_path: string;
    caption: string;
    doc_title: string;
    motif?: string;
}

const ImageGallery: React.FC = () => {
    const [images, setImages] = useState<AlchemyImage[]>([]);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(0);

    const fetchImages = async () => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/alchemy/images`, {
                params: { limit: 50, offset: page * 50 }
            });
            setImages(prev => [...prev, ...res.data]);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchImages();
    }, [page]);

    return (
        <div className="p-8 min-h-screen bg-slate-900 text-amber-50">
            <header className="mb-8 flex justify-between items-end border-b border-amber-900/30 pb-4">
                <div>
                    <h1 className="text-3xl font-serif text-amber-500 mb-2">The Gallery of Mutus Liber</h1>
                    <p className="text-slate-400 italic">"Read not the words, but the signs."</p>
                </div>
            </header>

            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {images.map(img => (
                    <div key={img.id} className="group relative aspect-square bg-black border border-amber-900/50 overflow-hidden cursor-pointer hover:border-amber-500 transition-all rounded-sm">
                        <img
                            src={img.image_path}
                            alt={img.caption}
                            className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity"
                        />
                        <div className="absolute inset-x-0 bottom-0 bg-black/80 p-2 translate-y-full group-hover:translate-y-0 transition-transform">
                            <p className="text-xs text-amber-200 truncate">{img.doc_title}</p>
                        </div>
                    </div>
                ))}
            </div>

            {loading && (
                <div className="flex justify-center p-8">
                    <Loader className="animate-spin text-amber-500" />
                </div>
            )}

            <div className="flex justify-center mt-8">
                <button
                    onClick={() => setPage(p => p + 1)}
                    className="px-6 py-2 border border-amber-700 text-amber-500 hover:bg-amber-900/20 transition-colors uppercase tracking-widest text-xs"
                >
                    Load More
                </button>
            </div>
        </div>
    );
};

export default ImageGallery;
