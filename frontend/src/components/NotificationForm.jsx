import React, { useState } from 'react';
import { motion } from 'framer-motion';

const NotificationForm = ({ onSubmit, onCancel }) => {
    const [email, setEmail] = useState('');
    const [telegram, setTelegram] = useState('');
    const [preference, setPreference] = useState('EMAIL'); // EMAIL, TELEGRAM, BOTH

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ email, telegram, preference });
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-xl mx-auto mt-8 bg-zinc-900 p-8 border border-zinc-800"
        >
            <h3 className="text-lg font-serif text-center mb-6 tracking-widest uppercase text-zinc-400">Complete Tracking</h3>
            <form onSubmit={handleSubmit} className="flex flex-col gap-6">
                <div>
                    <label className="block text-xs uppercase tracking-wider text-zinc-500 mb-2">Notification Method</label>
                    <div className="flex gap-4">
                        {['EMAIL', 'TELEGRAM', 'BOTH'].map((pref) => (
                            <button
                                key={pref}
                                type="button"
                                onClick={() => setPreference(pref)}
                                className={`flex-1 py-2 text-xs font-bold border ${preference === pref ? 'bg-zinc-800 border-zinc-500 text-white' : 'border-zinc-800 text-zinc-600'}`}
                            >
                                {pref}
                            </button>
                        ))}
                    </div>
                </div>

                {(preference === 'EMAIL' || preference === 'BOTH') && (
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email Address"
                        className="w-full bg-transparent border-b border-zinc-700 p-2 focus:outline-none focus:border-zinc-400 text-center"
                        required={preference === 'EMAIL'}
                    />
                )}

                {(preference === 'TELEGRAM' || preference === 'BOTH') && (
                    <input
                        type="text"
                        value={telegram}
                        onChange={(e) => setTelegram(e.target.value)}
                        placeholder="Telegram Chat ID"
                        className="w-full bg-transparent border-b border-zinc-700 p-2 focus:outline-none focus:border-zinc-400 text-center"
                        required={preference === 'TELEGRAM'}
                    />
                )}

                <div className="flex gap-4 mt-4">
                    <button type="button" onClick={onCancel} className="flex-1 py-4 uppercase text-xs tracking-widest text-zinc-500 hover:text-white transition-colors">
                        Cancel
                    </button>
                    <button type="submit" className="flex-1 bg-white text-black py-4 uppercase tracking-[0.2em] font-bold text-xs hover:bg-zinc-200 transition-colors">
                        Start Tracking
                    </button>
                </div>
            </form>
        </motion.div>
    );
};

export default NotificationForm;
