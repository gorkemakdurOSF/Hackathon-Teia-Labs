import React from "react";
import template from "./SearchBar.jsx";

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    this.ref = React.createRef();

    const { source, width } = props;
    this.state = { 
      source: ['own', 'store', 'both'].includes(source) ? source : 'own',
      searchString: "",
      width: width ? width : "100%",
    };
  }

  // TODO Add call for backend to perform search
  // Possible searches:
  // own - user wardrobe
  // store - stores products
  // both - perform the search with 'own' and 'store'
  search = (e) => {
    const { source } = this.state;
    if (e.key === "Enter") {
      console.log(e.key, source, this.ref.current.value.length);
    }

    if (this.ref.current) {
      this.setState({
        searchString: this.ref.current.value,
      });
    }
  };

  clear = () => {
    this.ref.current.value = "";
    this.setState({ searchString: "" });
  };

  render() {
    const { searchString, width } = this.state;
    return template(this.search, this.ref, searchString, this.clear, width);
  }
}

export default SearchBar;
