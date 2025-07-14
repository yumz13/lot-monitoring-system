import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { loadOven, unloadOven, emergencyStop } from '../store/actions/ovenActions';

const OvenControl = () => {
  const dispatch = useDispatch();
  const { ovens, loading } = useSelector(state => state.oven);
  const [lotNumber, setLotNumber] = useState('');
  const [ovenNumber, setOvenNumber] = useState(1);
  const [layerNumber, setLayerNumber] = useState(1);

  const handleLoadOven = () => {
    if (!lotNumber) {
      alert('Please enter a lot number');
      return;
    }
    
    dispatch(loadOven({
      lotNumber,
      ovenNumber,
      layerNumber
    }));
    
    setLotNumber('');
  };

  return (
    <div className="bg-white p-6 rounded shadow">
      <h3 className="text-lg font-semibold mb-4">Oven Control Panel</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-gray-700 mb-2">Lot Number</label>
          <input
            type="text"
            value={lotNumber}
            onChange={(e) => setLotNumber(e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2">Oven Number</label>
          <select
            value={ovenNumber}
            onChange={(e) => setOvenNumber(parseInt(e.target.value))}
            className="w-full p-2 border rounded"
          >
            {[...Array(10).keys()].map(i => (
              <option key={i+1} value={i+1}>Oven {i+1}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-gray-700 mb-2">Layer Number</label>
          <select
            value={layerNumber}
            onChange={(e) => setLayerNumber(parseInt(e.target.value))}
            className="w-full p-2 border rounded"
          >
            {[...Array(15).keys()].map(i => (
              <option key={i+1} value={i+1}>Layer {i+1}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="flex space-x-4">
        <button
          onClick={handleLoadOven}
          disabled={loading}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
        >
          Load Oven
        </button>
        
        <button
          onClick={() => dispatch(unloadOven(lotNumber))}
          disabled={loading || !lotNumber}
          className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700 disabled:bg-gray-400"
        >
          Unload Oven
        </button>
        
        <button
          onClick={() => dispatch(emergencyStop(ovenNumber))}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Emergency Stop
        </button>
      </div>
      
      <div className="mt-6">
        <h4 className="font-semibold mb-2">Oven Status</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {ovens && Object.entries(ovens).map(([ovenNum, layers]) => (
            <div key={ovenNum} className="bg-gray-50 p-3 rounded border">
              <h5 className="font-medium">Oven {ovenNum}</h5>
              {layers.map((layer, idx) => (
                <div key={idx} className="text-sm mt-2">
                  <p>Layer {layer.layer}: {layer.lot_number}</p>
                  <p className="text-gray-600">
                    {layer.remaining_minutes > 0 
                      ? `${layer.remaining_minutes} min remaining` 
                      : 'Ready'}
                  </p>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OvenControl;