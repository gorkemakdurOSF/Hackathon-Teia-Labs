import "./Navbar.scss";

import { Group, Navbar as MantineNavbar, Text, UnstyledButton } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass, faShoppingBag, faShirt } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="navbar">
      <MantineNavbar height={"100vh"} p="xs" width={{ base: 250 }}>
        <MantineNavbar.Section className="nav-brand">
          <Link to="/home">
            <h1>Fashionist</h1>
          </Link>
        </MantineNavbar.Section>
        <MantineNavbar.Section grow mt="md">
          <Group direction="column">
            <UnstyledButton className="nav-link">
              <Link to="/search">
                <Group>
                  <FontAwesomeIcon className="link-icon" icon={faMagnifyingGlass} />
                  <Text className="link-text" size="xl" weight={700}>Search</Text>
                </Group>
              </Link>
            </UnstyledButton>
            <UnstyledButton className="nav-link">
              <Link to="/shop">
                <Group>
                  <FontAwesomeIcon className="link-icon" icon={faShoppingBag} />
                  <Text className="link-text" size="xl" weight={700}>Shop</Text>
                </Group>
              </Link>
            </UnstyledButton>
            <UnstyledButton className="nav-link">
              <Link to="/wardrobe">
                <Group>
                  <FontAwesomeIcon className="link-icon" icon={faShirt} />
                  <Text className="link-text" size="xl" weight={700}>Wardrobe</Text>
                </Group>
              </Link>
            </UnstyledButton>
          </Group>
        </MantineNavbar.Section>
      </MantineNavbar>
    </div>
  );
}

export default Navbar;
