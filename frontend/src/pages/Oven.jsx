import React from 'react';
import OvenControl from '../components/OvenControl';

const Oven = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Oven Process</h1>
      <OvenControl />
    </div>
  );
};

export default Oven;