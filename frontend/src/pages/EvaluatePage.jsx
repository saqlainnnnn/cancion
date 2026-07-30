import { useState } from 'react';

const API_BASE = 'http://127.0.0.1:8015';

function EvaluatePage() {
  const [contractId, setContractId] = useState('');
  const [amount, setAmount] = useState('');
  const [status, setStatus] = useState('');
  const [contractVendor, setContractVendor] = useState('');
  const [contractAction, setContractAction] = useState('');
  const [evaluation, setEvaluation] = useState(null);

  const handleEvaluate = async (event) => {
    event.preventDefault();
    const trimmedContractId = contractId.trim();
    const parsedAmount = Number(amount);

    if (!trimmedContractId) {
      setStatus('Please enter a contract ID.');
      setEvaluation(null);
      return;
    }

    if (!amount || Number.isNaN(parsedAmount) || parsedAmount <= 0) {
      setStatus('Please enter a valid amount greater than 0.');
      setEvaluation(null);
      return;
    }

    try {
      setStatus('Loading contract details...');
      setContractVendor('');
      setContractAction('');

      const contractResponse = await fetch(`${API_BASE}/contracts/${trimmedContractId}`);
      if (!contractResponse.ok) {
        const data = await contractResponse.json();
        throw new Error(data.detail || 'Contract not found');
      }

      const contract = await contractResponse.json();
      setContractVendor(contract.vendor);
      setContractAction(contract.action);

      const response = await fetch(`${API_BASE}/governance/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contract_id: trimmedContractId,
          vendor: contract.vendor,
          action: contract.action,
          amount: { amount: parsedAmount, currency: 'USD' },
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Evaluation failed');
      }
      setEvaluation(data);
      setStatus(`Evaluation: ${data.outcome}`);
    } catch (error) {
      setStatus(error.message);
      setEvaluation(null);
    }
  };

  return (
    <div className="page-content">
      <section className="panel">
        <h2>Evaluate Spend Request</h2>
        <form onSubmit={handleEvaluate} className="form-group">
          <label>
            Contract ID
            <input
              value={contractId}
              onChange={(event) => setContractId(event.target.value)}
              placeholder="paste contract ID here"
            />
          </label>
          <label>
            Amount (USD)
            <input
              type="number"
              step="0.01"
              value={amount}
              onChange={(event) => setAmount(event.target.value)}
              placeholder="15.00"
            />
          </label>
          <button type="submit" className="primary">Evaluate</button>
        </form>

        {contractVendor && contractAction && (
          <div className="contract-summary">
            <p>Evaluating contract vendor: <strong>{contractVendor}</strong></p>
            <p>Action: <strong>{contractAction}</strong></p>
          </div>
        )}

        {evaluation && (
          <div className={`result ${evaluation.outcome.toLowerCase()}`}>
            <h3>Decision: {evaluation.outcome.toUpperCase()}</h3>
            {evaluation.reasons.length > 0 && (
              <ul className="reasons">
                {evaluation.reasons.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        {status && <p className="status">{status}</p>}
      </section>
    </div>
  );
}

export default EvaluatePage;
