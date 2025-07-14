import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createLotTraveler } from '../store/actions/lotActions';

const LotCreation = ({ processId, showMaterialFields = false }) => {
  const dispatch = useDispatch();
  const { customers, partNumbers } = useSelector(state => state.lot);
  const [formData, setFormData] = useState({
    customer_id: '',
    part_number_id: '',
    quantity: 1,
    material_length: '',
    material_weight: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'quantity' ? parseInt(value) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(createLotTraveler({
      ...formData,
      process_id: processId
    }));
  };

  return (
    <div className="bg-white p-6 rounded shadow">
      <h3 className="text-lg font-semibold mb-4">Create New Lot</h3>
      
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 gap-4 mb-4">
          <div>
            <label className="block text-gray-700 mb-2">Customer</label>
            <select
              name="customer_id"
              value={formData.customer_id}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Select Customer</option>
              {customers.map(customer => (
                <option key={customer.id} value={customer.id}>
                  {customer.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-gray-700 mb-2">Part Number</label>
            <select
              name="part_number_id"
              value={formData.part_number_id}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Select Part Number</option>
              {partNumbers
                .filter(pn => pn.customer_id === parseInt(formData.customer_id))
                .map(part => (
                  <option key={part.id} value={part.id}>
                    {part.part_number}
                  </option>
                ))}
            </select>
          </div>

          <div>
            <label className="block text-gray-700 mb-2">Quantity</label>
            <input
              type="number"
              name="quantity"
              min="1"
              value={formData.quantity}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>

          {showMaterialFields && (
            <>
              <div>
                <label className="block text-gray-700 mb-2">Material Length (mm)</label>
                <input
                  type="number"
                  name="material_length"
                  step="0.01"
                  value={formData.material_length}
                  onChange={handleChange}
                  className="w-full p-2 border rounded"
                />
              </div>

              <div>
                <label className="block text-gray-700 mb-2">Material Weight (g)</label>
                <input
                  type="number"
                  name="material_weight"
                  step="0.01"
                  value={formData.material_weight}
                  onChange={handleChange}
                  className="w-full p-2 border rounded"
                />
              </div>
            </>
          )}
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Create Lot
        </button>
      </form>
    </div>
  );
};

export default LotCreation;