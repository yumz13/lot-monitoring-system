import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { selectProcess, fetchProcesses } from '../store/actions/processActions';

const ProcessSelection = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { processes, loading, error } = useSelector(state => state.process);
  const { selectedArea } = useSelector(state => state.system);

  React.useEffect(() => {
    dispatch(fetchProcesses());
  }, [dispatch]);

  const handleProcessSelect = (processId) => {
    dispatch(selectProcess(processId));
    navigate('/login');
  };

  if (loading) return <div>Loading processes...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl font-semibold mb-4">Select Process for Area {selectedArea}</h2>
      
      <div className="flex flex-wrap gap-4">
        {processes.map(process => (
          <div 
            key={process.id}
            onClick={() => handleProcessSelect(process.id)}
            className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h3 className="font-semibold">{process.name}</h3>
            <p className="text-gray-600">{process.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProcessSelection;