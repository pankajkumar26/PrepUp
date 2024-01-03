import React, { useState, useEffect } from 'react';
import './style.css';

function Home() {

    return (
        <>
            
        <div className="OuterContainer">
            <section className="home">
                <span className="image">
                    <img className='contentLogo' src="logo.jpg" alt="" />
                </span>
                <h1 className="text">PrepUp</h1>
                <p className="text-small"></p>
            </section>

            <div className="container" style={{ display: option }}>
                <div className="tiles">
                    <a className="tile makeFood">
                        <span className="tile-title">Interview Prep</span>
                    </a>

                    <a className="tile requiredFood">
                        <span className="tile-title">Article Generator</span>
                    </a>

                    <a href="http://localhost:8000/" >
                        <div className="tile saveFood">
                            <span className="tile-title">Chat with PDF</span>
                        </div>
                    </a>

                    <div className="tile foodExpiry">
                        <span className="tile-title">Text Summarizer</span>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}

export default Home;


