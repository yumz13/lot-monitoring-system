import React from 'react';
import DefectInput from '../components/DefectInput';
import { useSelector } from 'react-redux';

const AssemblyInspection = () => {
  const { currentProcess } = useSelector(state => state.system);
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Assembly Inspection</h1>
      
      <div className="bg-white p-6 rounded shadow">
        <DefectInput processId={currentProcess} />
      </div>
    </div>
  );
};

export default AssemblyInspection;