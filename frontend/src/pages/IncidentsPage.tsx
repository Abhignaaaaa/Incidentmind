import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Incident {
  id: number;
  title: string;
  service: string;
  severity: string;
  root_cause?: string;
}

const IncidentsPage: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8001/api/incidents')
      .then(res => setIncidents(res.data))
      .catch(err => console.error("Error fetching incidents", err));
  }, []);

  return (
    <div>
      <h2>Incidents</h2>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Service</th>
            <th>Severity</th>
            <th>Root Cause</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map(inc => (
            <tr key={inc.id}>
              <td>{inc.id}</td>
              <td>{inc.title}</td>
              <td>{inc.service}</td>
              <td>{inc.severity}</td>
              <td>{inc.root_cause || 'Unknown'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default IncidentsPage;
