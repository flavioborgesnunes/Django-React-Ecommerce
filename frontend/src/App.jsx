import { useState } from 'react'
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Login from './views/auth/Login'
import Register from './views/auth/Register'
import Dashboard from './views/auth/Dashboard'
import Logout from './views/auth/Logout'
import ForgotPassword from './views/auth/ForgotPassword'
import CreatePassword from './views/auth/CreatePassword'
import StoreHeader from './views/base/StoreHeader'
import Storefooter from './views/base/StoreFooter'
import MainWrapper from './layout/mainWrapper'
import Products from './views/store/Products'
import ProductDetail from './views/store/ProductDetail'
import Cart from './views/store/Cart'

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <StoreHeader />
      <MainWrapper>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/create-new-password" element={<CreatePassword />} />

          {/* Store Components */
          }
          <Route path="/" element={<Products />} />
          <Route path="/detail/:slug/" element={<ProductDetail />} />
          <Route path="/cart/" element={<Cart />} />

        </Routes>
      </MainWrapper>
      <Storefooter />
    </BrowserRouter>

  )
}

export default App
