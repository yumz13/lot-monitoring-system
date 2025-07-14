import React from 'react';
import DefectInput from '../components/DefectInput';
import { useSelector } from 'react-redux';

const QCInspection = () => {
  const { currentProcess } = useSelector(state => state.system);
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">QC/QA Inspection</h1>
      
      <div className="bg-white p-6 rounded shadow">
        <DefectInput processId={currentProcess} isFinalInspection />
      </div>
    </div>
  );
};

export default QCInspection;