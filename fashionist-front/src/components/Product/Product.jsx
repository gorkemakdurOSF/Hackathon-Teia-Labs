import "./Product.scss";
import React, { useState } from "react";

import { Image, Group } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as heartFull, faShoppingBag, faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { faHeart as heartEmpty, faCircle } from "@fortawesome/free-regular-svg-icons";

function Product(props) {
    const { id, liked, isLikeable, isShoppable, isSelectable, add, remove, url } = props;
    let { ndUrl } = props;
    const [isLike, like] = useState(liked);
    const [isHover, hover] = useState(false);
    const [isSelect, select] = useState(false);

    ndUrl = !ndUrl ? url : ndUrl

    return (
        <div className="product">
            <div className="product-icons">
                <Group className="icons" spacing="xs">
                    {
                        isShoppable
                        && (
                            <FontAwesomeIcon
                                className="shop-icon icon"
                                icon={faShoppingBag}
                            />
                        )
                    }
                    {
                        isLikeable
                        && (
                            <FontAwesomeIcon
                                className={`like-icon icon ${!isLike ? "not-liked" : "liked"}`}
                                icon={!isLike ? heartEmpty : heartFull}
                                onClick={() => like(!isLike)}
                            />
                        )
                    }
                    {
                        isSelectable
                        && (
                            <FontAwesomeIcon
                                className={`select-icon icon ${!isSelect ? "not-selected" : "selected"}`}
                                icon={!isSelect ? faCircle : faCircleCheck}
                                onClick={() => {
                                    !isSelect ? add(id) : remove(id)
                                    select(!isSelect)
                                }}
                            />
                        )
                    }
                </Group>
            </div>
            <Image
                src={!isHover ? url : ndUrl}
                alt="product image"
                className="product-image"
                onMouseEnter={() => hover(true)}
                onMouseLeave={() => hover(false)}
                onClick={isSelectable ? () => {
                    !isSelect ? add(id) : remove(id)
                    select(!isSelect)
                } : ""}
                style={{ cursor: isSelectable ? "pointer" : "" }}
            />
        </div>
    );
};

export default Product;
