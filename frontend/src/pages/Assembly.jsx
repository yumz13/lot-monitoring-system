import React from 'react';
import LotCreation from '../components/LotCreation';
import DefectInput from '../components/DefectInput';
import { useSelector } from 'react-redux';

const Assembly = () => {
  const { currentProcess } = useSelector(state => state.system);
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Assembly Process</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LotCreation processId={currentProcess} />
        <DefectInput processId={currentProcess} />
      </div>
    </div>
  );
};

export default Assembly;