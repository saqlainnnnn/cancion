import { useEffect, useState } from 'react';

const API_BASE = 'http://127.0.0.1:8015';

function HistoryPage() {
  const [contracts, setContracts] = useState([]);
  const [status, setStatus] = useState('Loading...');

  const loadInactiveContracts = async () => {
    try {
      const response = await fetch(`${API_BASE}/contracts/history/inactive`);
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Unable to load history');
      }
      const data = await response.json();
      setContracts(data);
      setStatus(`Loaded ${data.length} inactive contracts`);
    } catch (error) {
      setStatus(error.message);
    }
  };

  useEffect(() => {
    loadInactiveContracts();
  }, []);

  return (
    <div className="page-content">
      <section className="panel">
        <h2>History</h2>
        <p className="status">{status}</p>
        {contracts.length === 0 ? (
          <p className="empty-state">No inactive contracts yet.</p>
        ) : (
          <ul className="contract-list">
            {contracts.map((contract) => (
              <li key={contract.id} className="contract-card">
                <div className="contract-info">
                  <h3>{contract.vendor}</h3>
                  <p className="contract-meta">
                    <span className="action">{contract.action}</span>
                    <span className="status-badge">{contract.status}</span>
                  </p>
                  <p className="contract-meta contract-id-meta">
                    <span className="uuid-id" title={contract.id}>{contract.id}</span>
                  </p>
                  <p className="contract-amount">
                    Limit: <strong>${contract.max_amount.amount}</strong> {contract.max_amount.currency}/mo
                  </p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default HistoryPage;
