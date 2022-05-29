import { Routes, Route } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Home from './pages/Home';
import Shop from './pages/Shop';
import Wardrobe from './pages/Wardrobe';
import InsertProduct from './pages/InsertProduct';
import CreateOutfit from './pages/CreateOutfit';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="home" element={<Home />} />
        <Route path="shop" element={<Shop />} />
        <Route path="wardrobe" element={<Wardrobe />} />
        <Route path="insert" element={<InsertProduct />} />
        <Route path="create/outfit" element={<CreateOutfit />} />
      </Routes>
    </div>
  );
}

export default App;
