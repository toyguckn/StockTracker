import React, { useState } from 'react';
import ProductForm from './components/ProductForm';
import SizeSelector from './components/SizeSelector';
import NotificationForm from './components/NotificationForm';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

// Configure Axios
const api = axios.create({
  baseURL: 'http://localhost:8080/api', // Update in prod
});

function App() {
  const [step, setStep] = useState(1); // 1: URL, 2: Size, 3: Notify, 4: Success
  const [url, setUrl] = useState('');
  const [sizes, setSizes] = useState([]);
  const [selectedSize, setSelectedSize] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUrlSubmit = async (submittedUrl) => {
    setIsLoading(true);
    setError('');
    try {
      const response = await api.post('/products/check-sizes', { url: submittedUrl });
      setSizes(response.data);
      setUrl(submittedUrl);
      setStep(2);
    } catch (err) {
      setError('Failed to fetch sizes. Please check the URL.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSizeConfirm = () => {
    if (selectedSize) setStep(3);
  };

  const handleNotificationSubmit = async (data) => {
    setIsLoading(true);
    try {
      await api.post('/tracking', {
        url,
        size: selectedSize,
        email: data.email,
        telegramChatId: data.telegram,
        preference: data.preference
      });
      setStep(4);
    } catch (err) {
      setError('Failed to create tracking. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    setStep(1);
    setUrl('');
    setSizes([]);
    setSelectedSize('');
    setError('');
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-4 selection:bg-white selection:text-black">
      <header className="absolute top-8 w-full text-center">
        <h1 className="text-3xl font-serif tracking-[0.3em] uppercase">ZARA STOCK TRACKER</h1>
      </header>

      <main className="w-full max-w-4xl relative">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="intro" exit={{ opacity: 0, y: -20 }} className="flex flex-col items-center">
              <p className="text-zinc-500 mb-12 text-center max-w-md font-light">
                Never miss a restock again. Enter a product link to get instant notifications when your size is back.
              </p>
              <ProductForm onUrlSubmit={handleUrlSubmit} isLoading={isLoading} />
            </motion.div>
          )}

          {step === 2 && (
            <SizeSelector
              sizes={sizes}
              selectedSize={selectedSize}
              onSelectSize={setSelectedSize}
              onConfirm={handleSizeConfirm}
            />
          )}

          {step === 3 && (
            <NotificationForm onSubmit={handleNotificationSubmit} onCancel={() => setStep(2)} />
          )}

          {step === 4 && (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
              </div>
              <h2 className="text-2xl font-serif uppercase tracking-widest mb-4">Tracking Active</h2>
              <p className="text-zinc-500 mb-8">We'll notify you as soon as it's back in stock.</p>
              <button onClick={reset} className="text-sm underline underline-offset-4 decoration-zinc-700 hover:text-white transition-colors">Track Another Item</button>
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="absolute -bottom-24 left-0 right-0 text-center text-rose-500 text-sm tracking-wide"
          >
            {error}
          </motion.div>
        )}
      </main>

      <footer className="absolute bottom-6 w-full text-center text-[10px] text-zinc-700 uppercase tracking-widest">
        ZST © 2026 • Automated Intelligence
      </footer>
    </div>
  );
}

export default App;
