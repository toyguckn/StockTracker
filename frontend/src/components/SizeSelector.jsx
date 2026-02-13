import React from 'react';
import { motion } from 'framer-motion';

const SizeSelector = ({ sizes, productInfo, selectedSize, onSelectSize, onConfirm }) => {
    if (!sizes || sizes.length === 0) return null;

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-xl mx-auto mt-12 bg-zinc-900 p-8 border border-zinc-800"
        >
            {/* Product Info */}
            {(productInfo?.name || productInfo?.image) && (
                <div className="flex items-center gap-6 mb-8 pb-6 border-b border-zinc-800">
                    {productInfo.image && (
                        <img
                            src={productInfo.image}
                            alt={productInfo.name || 'Product'}
                            className="w-24 h-32 object-cover border border-zinc-700"
                            onError={(e) => { e.target.style.display = 'none'; }}
                        />
                    )}
                    <div className="flex-1 min-w-0">
                        <p className="text-xs text-zinc-500 uppercase tracking-widest mb-1">Product</p>
                        <h3 className="text-lg font-serif text-zinc-200 leading-tight">
                            {productInfo.name || 'Unknown Product'}
                        </h3>
                    </div>
                </div>
            )}

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
