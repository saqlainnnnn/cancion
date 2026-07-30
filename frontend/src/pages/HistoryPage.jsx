import { useEffect, useState } from 'react';

const API_BASE = 'http://127.0.0.1:8015';

function HistoryPage() {
  const [inactiveContracts, setInactiveContracts] = useState([]);
  const [status, setStatus] = useState('Loading...');

  const loadInactiveContracts = async () => {
    try {
      const response = await fetch(`${API_BASE}/contracts/history/inactive`);
      const data = await response.json();
      setInactiveContracts(data);
      setStatus(`Loaded ${data.length} inactive contracts`);
    } catch (error) {
      setStatus(`Unable to reach backend: ${error.message}`);
    }
  };

  useEffect(() => {
    loadInactiveContracts();
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const calculateNextRenewal = (createdAt, frequency) => {
    const date = new Date(createdAt);
    switch (frequency) {
      case 'DAILY':
        date.setDate(date.getDate() + 1);
        break;
      case 'WEEKLY':
        date.setDate(date.getDate() + 7);
        break;
      case 'MONTHLY':
        date.setMonth(date.getMonth() + 1);
        break;
      case 'QUARTERLY':
        date.setMonth(date.getMonth() + 3);
        break;
      case 'ANNUALLY':
      case 'YEARLY':
        date.setFullYear(date.getFullYear() + 1);
        break;
      default:
        return 'Unknown';
    }
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="page-content">
      <section className="panel">
        <h2>Deactivated Contracts History</h2>
        <p className="status">{status}</p>
        {inactiveContracts.length === 0 ? (
          <p className="empty-state">No deactivated contracts yet.</p>
        ) : (
          <ul className="contract-list history-list">
            {inactiveContracts.map((contract) => (
              <li key={contract.id} className="contract-card history-card">
                <div className="contract-info">
                  <h3>{contract.vendor}</h3>
                  <p className="contract-meta">
                    <span className="action">{contract.action}</span>
                    <span className="status-badge inactive">{contract.status}</span>
                  </p>
                  <p className="contract-amount">
                    Limit: <strong>${contract.max_amount.amount}</strong> {contract.max_amount.currency}/{contract.frequency.toLowerCase()}
                  </p>
                  <div className="contract-dates">
                    <div className="date-item">
                      <span className="date-label">Created:</span>
                      <span className="date-value">{formatDate(contract.created_at)}</span>
                    </div>
                    <div className="date-item">
                      <span className="date-label">Next Renewal:</span>
                      <span className="date-value">{calculateNextRenewal(contract.created_at, contract.frequency)}</span>
                    </div>
                  </div>
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
