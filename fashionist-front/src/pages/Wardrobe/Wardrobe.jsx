import "./Wardrobe.scss";
import React from "react";

import Navbar from "../../components/Navbar";

import { Group, Container } from "@mantine/core";

function template() {
  return (
    <div className="wardrobe">
      <Group>
        <Navbar />
        <Container fluid className="wardrobe-content">
          <h1>Outfits</h1>
        </Container>
      </Group>
    </div>
  );
};

export default template;
