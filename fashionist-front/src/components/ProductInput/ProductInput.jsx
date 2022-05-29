import "./ProductInput.scss";
import React from "react";

import { Grid, NativeSelect, Text } from "@mantine/core";

function ProductInput(props) {
  let { key, value } = props;
  key = !key ? "{KEY}" : key;
  value = !value ? ["{VALUE}", "{VALUE}", "{VALUE}", "{VALUE}"] : value;

  return (
    <Grid className="product-input">
      <Grid.Col span={4}>
        <Text weight={700}>
          {key}
        </Text>
      </Grid.Col>
      <Grid.Col span={8}>
        <NativeSelect data={value} />
      </Grid.Col>
    </Grid>
  );
};

export default ProductInput;
