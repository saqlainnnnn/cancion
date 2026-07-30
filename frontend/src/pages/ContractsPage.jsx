import { useEffect, useState } from 'react';

const API_BASE = 'http://127.0.0.1:8015';

function ContractsPage() {
  const [contracts, setContracts] = useState([]);
  const [status, setStatus] = useState('Loading...');
  const [form, setForm] = useState({
    text: 'renew Netflix for $15 monthly',
  });

  const loadContracts = async () => {
    try {
      const response = await fetch(`${API_BASE}/contracts/`);
      const data = await response.json();
      setContracts(data);
      setStatus(`Loaded ${data.length} contracts`);
    } catch (error) {
      setStatus(`Unable to reach backend: ${error.message}`);
    }
  };

  useEffect(() => {
    loadContracts();
  }, []);

  const handleCreateContract = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(`${API_BASE}/contracts/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create contract');
      }
      setStatus(`Created contract for ${data.vendor}`);
      setForm({ text: '' });
      loadContracts();
    } catch (error) {
      setStatus(error.message);
    }
  };

  const handleDeleteContract = async (contractId) => {
    try {
      const response = await fetch(`${API_BASE}/contracts/${contractId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to deactivate contract');
      }
      setStatus('Contract deactivated');
      loadContracts();
    } catch (error) {
      setStatus(error.message);
    }
  };

  return (
    <div className="page-content">
      <section className="panel">
        <h2>Create Contract</h2>
        <form onSubmit={handleCreateContract} className="form-group">
          <label>Describe the spending intent (e.g., "renew Netflix for $15 monthly")</label>
          <textarea
            value={form.text}
            onChange={(event) => setForm({ ...form, text: event.target.value })}
            placeholder="e.g., renew Netflix for $15 monthly"
            rows="3"
          />
          <button type="submit" className="primary">Create Contract</button>
        </form>
      </section>

      <section className="panel">
        <h2>Active Contracts</h2>
        <p className="status">{status}</p>
        {contracts.length === 0 ? (
          <p className="empty-state">No contracts yet. Create one above.</p>
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
                  <p className="contract-amount">
                    Limit: <strong>${contract.max_amount.amount}</strong> {contract.max_amount.currency}/mo
                  </p>
                </div>
                <button
                  type="button"
                  className="delete-btn"
                  onClick={() => handleDeleteContract(contract.id)}
                  title="Deactivate this contract"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

export default ContractsPage;
