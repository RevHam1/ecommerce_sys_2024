import { useEffect } from 'react';
// import { LoggedOutView } from '../shop/home';
import { Link } from 'react-router-dom';
import { logout } from '../../utils/auth';


const Logout = () => {
    useEffect(() => {
        logout();
    }, []);
    return (
        <>
            <section>
                <main className="" style={{ marginBottom: 400, marginTop: 150 }}>
                    <div className="container">
                        <section className="">
                            <div className="row d-flex justify-content-center">
                                <div className="col-xl-5 col-md-8">
                                    <div className="card rounded-5">
                                        <div className="card-body p-4">
                                            <h3 className="text-center">You have been logged out</h3>
                                            <div className="d-flex justify-content-center" >
                                                <Link to="/login" className='btn btn-primary me-2'>Login <i className='fas fa-sign-in-alt'></i> </Link>
                                                <Link to="/login" className='btn btn-primary'>Register <i className='fas fa-user-plus'></i> </Link>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </main>
            </section>
        </>
    );
};

export default Logout;

// import { useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import { logout } from '../../utils/auth';
// // import { LoggedOutView } from '../shop/home';

// const Logout = () => {
//   useEffect(() => {
//     logout();
//   }, []);

//   return (
//     <div>
//       <h1>Logged Out</h1>
//       <Link to={'/register'}>Register</Link>
//         <br />
//       <Link to={'/login'} >Login</Link>
//     </div>
//   )
// }

// export default Logout


