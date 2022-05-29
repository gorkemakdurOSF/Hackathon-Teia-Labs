import "./SearchBar.scss";
import React from "react";

import { TextInput } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass, faXmark } from "@fortawesome/free-solid-svg-icons";

function template(search, ref, searchString, clear, width) {
  return (
    <div className="search-bar" style={{ width: width }}>
      <TextInput
        ref={ref}
        placeholder="Search"
        icon={<FontAwesomeIcon icon={faMagnifyingGlass} />}
        rightSection={
          searchString.length > 0 ?
            <FontAwesomeIcon style={{ cursor: "pointer" }} icon={faXmark} onClick={clear} /> :
            ""
        }
        onKeyUp={search}
      />
    </div>
  );
};

export default template;
