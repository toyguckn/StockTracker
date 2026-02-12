import React, { useState } from 'react';
import { motion } from 'framer-motion';

const ProductForm = ({ onUrlSubmit, isLoading }) => {
    const [url, setUrl] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (url) onUrlSubmit(url);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-xl mx-auto"
        >
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <label className="text-xl font-serif text-center mb-2 tracking-widest text-zinc-400">ENTER PRODUCT URL</label>
                <div className="relative group">
                    <input
                        type="url"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://www.zara.com/..."
                        className="w-full bg-zinc-900 border border-zinc-700 p-4 rounded-none focus:outline-none focus:border-zinc-400 text-center transition-all duration-300 group-hover:border-zinc-600"
                        required
                    />
                    <div className="absolute inset-0 border border-transparent group-hover:border-zinc-600 pointer-events-none transition-all duration-500"></div>
                </div>
                <button
                    type="submit"
                    disabled={isLoading}
                    className="bg-white text-black py-4 px-8 uppercase tracking-[0.2em] font-bold text-sm hover:bg-zinc-200 transition-colors disabled:opacity-50"
                >
                    {isLoading ? 'Checking...' : 'Check Availability'}
                </button>
            </form>
        </motion.div>
    );
};

export default ProductForm;
