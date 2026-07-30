import { useState } from 'react';
import ContractsPage from './pages/ContractsPage';
import HistoryPage from './pages/HistoryPage';
import EvaluatePage from './pages/EvaluatePage';

const NAV_ITEMS = [
  { key: 'contracts', label: 'Contracts' },
  { key: 'history', label: 'History' },
  { key: 'evaluate', label: 'Evaluate' },
];

function App() {
  const [activePage, setActivePage] = useState('contracts');

  const renderPage = () => {
    switch (activePage) {
      case 'history':
        return <HistoryPage />;
      case 'evaluate':
        return <EvaluatePage />;
      default:
        return <ContractsPage />;
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <h1>Cancion</h1>
          <p>Spend governance</p>
        </div>
        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.key}
              type="button"
              className={item.key === activePage ? 'nav-item active' : 'nav-item'}
              onClick={() => setActivePage(item.key)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </aside>
      <main className="content-area">{renderPage()}</main>
    </div>
  );
}

export default App;
