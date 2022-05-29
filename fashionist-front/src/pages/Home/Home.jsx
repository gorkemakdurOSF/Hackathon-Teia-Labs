import "./Home.scss";
import React from "react";

import Navbar from "../../components/Navbar";
import Product from "../../components/Product";
import SearchBar from "../../components/SearchBar";
import FloatingActionButton from "../../components/FloatingActionButton";

import { Grid, Group, Container } from "@mantine/core";

function template(clothes) {
    return (
        <div className="home">
            <Group>
                <Navbar />
                <Container fluid className="home-content">
                    <Group className="content" direction="column">
                        <h1 className="content-title">Home</h1>
                        <SearchBar />
                        <div className="content-content">
                            <Grid>
                                {
                                    clothes.map(c => {
                                        return (
                                            <Grid.Col span={3}>
                                                <Product
                                                    id={c._id}
                                                    liked={c.isLiked}
                                                    url={c.url}
                                                    isLikeable
                                                />
                                            </Grid.Col>
                                        )
                                    })
                                }
                            </Grid>
                        </div>
                    </Group>
                </Container>
            </Group>
            <FloatingActionButton />
        </div>
    );
};

export default template;
