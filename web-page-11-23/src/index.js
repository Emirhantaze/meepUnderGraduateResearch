import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import DataContextProvider from './Datacontext';
import SelectioncontextProvider from './Selectionconcext';
import 'bootstrap/dist/css/bootstrap.min.css';
import ViewportProvider from './ViewPortContext';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(

  <SelectioncontextProvider>

    <DataContextProvider>
      <ViewportProvider>
        <App />
      </ViewportProvider>
    </DataContextProvider>

  </SelectioncontextProvider>
);