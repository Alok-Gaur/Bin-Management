import React, { useState } from 'react'
import "./LoginSignup.css"
import axios from 'axios'

export const LoginSignup = () => {
  
    const [action, setAction] = useState("Sign Up");

    const [credentials, setCredentials] = useState({
        username:"",
        email:"",
        password: "",
    })

    const handleChanges = (e)=>{
        const {name, value} = e.target;
        // setCredentials(...credentials, name:value);
        setCredentials((prev)=>{
            return{...prev, [name]:value}
        })
    }

    const clearChanges = ()=>{
        setCredentials(()=>{
            return {username: '',
            email: '',
            password: '',
        }})
    }
    
    // This is used to signup the user
    const SignUp = async ()=>{
        try{
            const response= await axios.post("http://127.0.0.1:8000/user/signup/",
                credentials,
                {
                    headers: {
                        "Content-Type": "application/json", // Required for JSON data
                    },
                }
            );
            console.log(response);
            localStorage.setItem('authToken', response['data']['token'])
        }
        catch (error){
            console.error(error)
        }
        clearChanges();
    }

    // Function to Login the User
    const Login = async ()=>{
        try{
            const response = await axios.post("http://127.0.0.1:8000/user/login/",
                {
                    "email_or_username": credentials.email,
                    "password": credentials.password
                }, 
                {
                    headers:{
                        "Content-Type": "application/json",
                    },
                }
            );
            console.log(response);
            localStorage.setItem("authToken", response["data"]["Token"])            
        }
        catch (error){
            console.log(error)
        }
        clearChanges();
    }

    // Toggle 
    const manageSignup = ()=>{
        if (action === "Login"){
            setAction("Sign Up")
        }
        else {
            SignUp();
        }
    }

    const manageLogin = ()=>{
        if (action === "Sign Up"){
            setAction("Login")
        }
        else {
            Login();
        }
    }

    return (
    <div className="container">
        <div className="header">
            <div className="text">{action}</div>
            <div className="underline"></div>
        </div>
        <div className="inputs">
            {action==="Login"?<div></div>:<div className="input">
                <label htmlFor="username">Username</label>
                <input type="text" name="username" placeholder='Name' onChange={handleChanges} value={credentials.username}/>
            </div>}
            <div className="input">
                <label htmlFor="email">{action==="Sign Up"?"Email":"Username/Email"}</label>
                <input type={action==="Login"?"text":"email"} name="email" placeholder='email' onChange={handleChanges} value={credentials.email}/>
            </div>
            <div className="input">
                <label htmlFor="password">Password</label>
                <input type="password" name="password" placeholder='password' onChange={handleChanges} value={credentials.password}/>
            </div>
        </div>
        {action==="Sign Up"?<div></div>:<div className="forgot-passwod">Forgot Passwod? <span>Click Here!</span></div>}
        <div className="submit-container">
            <div className={action==="Login"?"submit gray":"submit"} onClick={manageSignup}>Sign Up</div>
            <div className={action==="Sign Up"?"submit gray":"submit"} onClick={manageLogin}>Login</div>
        </div>
    </div>
  )
}
