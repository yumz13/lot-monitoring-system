import React from 'react';
import LotCreation from '../components/LotCreation';
import { useSelector } from 'react-redux';

const MaterialPrep = () => {
  const { currentProcess } = useSelector(state => state.system);
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Material Preparation</h1>
      
      <div className="bg-white p-6 rounded shadow">
        <LotCreation processId={currentProcess} showMaterialFields />
      </div>
    </div>
  );
};

export default MaterialPrep;