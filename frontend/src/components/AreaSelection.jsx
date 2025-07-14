import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAreas, selectArea } from '../store/actions/areaActions';
import { useNavigate } from 'react-router-dom';

const AreaSelection = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { areas, loading, error } = useSelector(state => state.areas);

  React.useEffect(() => {
    dispatch(fetchAreas());
  }, [dispatch]);

  const handleAreaSelect = (areaId) => {
    dispatch(selectArea(areaId));
    navigate('/process-selection');
  };

  if (loading) return <div>Loading areas...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {areas.map(area => (
        <div 
          key={area.id}
          onClick={() => handleAreaSelect(area.id)}
          className="bg-white p-6 rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
        >
          <h3 className="text-xl font-semibold">{area.name}</h3>
          <p className="text-gray-600">{area.description}</p>
        </div>
      ))}
    </div>
  );
};

export default AreaSelection;