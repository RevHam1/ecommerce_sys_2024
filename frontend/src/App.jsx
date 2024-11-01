// import { useState } from 'react'
import { BrowserRouter, Route, Routes } from "react-router-dom";

import Mainwrapper from "./layout/Mainwrapper";
import CreatePassword from "./views/auth/CreatePassword";
import Dashboard from "./views/auth/Dashboard";
import ForgotPassword from "./views/auth/ForgotPassword";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";
import Register from "./views/auth/Register";
import StoreFooter from "./views/base/StoreFooter";
import StoreHeader from "./views/base/StoreHeader";
import ProductDetail from "./views/store/ProductDetail";
import Products from "./views/store/Products";

function App() {
  return (
    <BrowserRouter>
      <StoreHeader />
      <Mainwrapper>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/create-new-password" element={<CreatePassword />} />

          {/* Store Components*/}
          <Route path="/" element={<Products />} />
          <Route path="/detail/:slug/" element={<ProductDetail />} />
        </Routes>
      </Mainwrapper>
      <StoreFooter />
    </BrowserRouter>
  );
}

export default App;
