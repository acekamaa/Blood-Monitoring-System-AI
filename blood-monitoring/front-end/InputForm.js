// src/InputForm.js
import React, { useState } from 'react';

function InputForm() {
  const [formData, setFormData] = useState({ bloodType: '', county: '', date: '' });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:5000/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
      .then(response => response.json())
      .then(data => alert(data.message))
      .catch(error => alert('Error: ' + error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <select name="bloodType" onChange={handleChange}>
        <option value="">Select Blood Type</option>
        <option value="A+">A+</option>
        <option value="O-">O-</option>
        {/* Add all blood types */}
      </select>
      <input type="text" name="county" placeholder="County" onChange={handleChange} />
      <input type="date" name="date" onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}

export default InputForm;