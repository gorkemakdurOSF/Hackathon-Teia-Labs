import "./InsertProduct.scss";
import React from "react";

import Navbar from "../../components/Navbar";
import DragAndDropZone from "../../components/DragAndDropZone";

import { Container, Group } from "@mantine/core";

function template() {
  return (
    <div className="insert-product">
      <Group>
        <Navbar />
        <Container className="insert-content">
          <Group position="center" direction="column">
            <h1>Let's add some clothes</h1>
            <DragAndDropZone />
          </Group>
        </Container>
      </Group>
    </div>
  );
};

export default template;
