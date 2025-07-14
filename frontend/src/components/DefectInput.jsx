import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logDefect } from '../store/actions/defectActions';

const DefectInput = ({ lotId, processId }) => {
  const dispatch = useDispatch();
  const { defectCodes } = useSelector(state => state.defect);
  const [selectedDefects, setSelectedDefects] = useState([]);
  const [notes, setNotes] = useState('');

  const handleDefectToggle = (defectId) => {
    setSelectedDefects(prev => 
      prev.includes(defectId) 
        ? prev.filter(id => id !== defectId) 
        : [...prev, defectId]
    );
  };

  const handleSubmit = () => {
    if (selectedDefects.length === 0) {
      alert('Please select at least one defect');
      return;
    }
    
    dispatch(logDefect({
      lotId,
      processId,
      defectCodes: selectedDefects,
      notes
    }));
    
    setSelectedDefects([]);
    setNotes('');
  };

  return (
    <div className="bg-white p-4 rounded shadow">
      <h3 className="text-lg font-semibold mb-4">Defect Input</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {defectCodes.map(defect => (
          <div 
            key={defect.id}
            onClick={() => handleDefectToggle(defect.id)}
            className={`p-3 border rounded cursor-pointer ${
              selectedDefects.includes(defect.id) 
                ? 'bg-red-100 border-red-500' 
                : 'hover:bg-gray-50'
            }`}
          >
            <div className="font-semibold">{defect.code}</div>
            <div className="text-sm text-gray-600">{defect.description}</div>
          </div>
        ))}
      </div>
      
      <textarea
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Additional notes..."
        className="w-full p-2 border rounded mb-4"
      />
      
      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Submit Defects
      </button>
    </div>
  );
};

export default DefectInput;