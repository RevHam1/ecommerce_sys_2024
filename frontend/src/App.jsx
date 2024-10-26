// import { useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Mainwrapper from './layout/Mainwrapper';
import CreatePassword from './views/auth/CreatePassword';
import Dashboard from './views/auth/Dashboard';
import ForgotPassword from './views/auth/ForgotPassword';
import Login from './views/auth/Login';
import Logout from './views/auth/Logout';
import Register from './views/auth/Register';
import StoreFooter from './views/base/StoreFooter';
import StoreHeader from './views/base/StoreHeader';

function App() {

  return (
    <BrowserRouter>
      <StoreHeader />
      <Mainwrapper>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/create-new-password" element={<CreatePassword />} />
        </Routes>
      </Mainwrapper>
      <StoreFooter />
    </BrowserRouter>
  )
}

export default App
