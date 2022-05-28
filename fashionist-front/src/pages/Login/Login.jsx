import "./Login.scss";
import React from "react";

import image from '../../assets/login.jpg';
import { Button, Center } from "@mantine/core";
import { Link } from "react-router-dom";

function template() {
  return (
    <div className="login" style={{ backgroundImage: `url(${image})` }}>
      <div className="blur" />
      <Center className="login-content">
        <Button>
          <Link to="home">
            Login
          </Link>
        </Button>
      </Center>
    </div>
  );
};

export default template;
