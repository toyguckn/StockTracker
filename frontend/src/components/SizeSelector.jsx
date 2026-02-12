import React from 'react';
import { motion } from 'framer-motion';

const SizeSelector = ({ sizes, selectedSize, onSelectSize, onConfirm }) => {
    if (!sizes || sizes.length === 0) return null;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-xl mx-auto mt-12 bg-zinc-900 p-8 border border-zinc-800"
        >
            <h3 className="text-lg font-serif text-center mb-6 tracking-widest uppercase text-zinc-400">Select Size</h3>
            <div className="grid grid-cols-4 gap-4 mb-8">
                {sizes.map((size) => (
                    <button
                        key={size}
                        onClick={() => onSelectSize(size)}
                        className={`p-4 border text-sm font-bold transition-all duration-300 ${selectedSize === size
                                ? 'bg-white text-black border-white'
                                : 'bg-transparent text-zinc-400 border-zinc-700 hover:border-zinc-500'
                            }`}
                    >
                        {size}
                    </button>
                ))}
            </div>

            {selectedSize && (
                <button
                    onClick={onConfirm}
                    className="w-full bg-emerald-600 text-white py-4 uppercase tracking-[0.2em] font-bold text-sm hover:bg-emerald-500 transition-colors"
                >
                    Track Stock
                </button>
            )}
        </motion.div>
    );
};

export default SizeSelector;
