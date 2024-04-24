import React from 'react';

class Search extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fieldText: '',
            jData: ''
        }
    }

    handleSearch = () => {
        console.log(this.state.fieldText);
        const artist = this.state.fieldText;
        fetch(`http://127.0.0.1:5000/artists?name=${artist}`, {

        }).then(response => {
            if (response.status === 200) {
                return response.json();
            } else {
                window.alert(`Failed searching for ${artist}`)
            }
        }).then(json => {
            this.props.onSearch(json);
        })
    }

    handleText = (event) => {
        const value = event.target.value;
        this.setState({fieldText: value});
    }

    render() {
        return (
            <>
            <div className='search-div'>
                <input value={this.state.fieldText} onChange={this.handleText} type='text' placeholder='Enter Artist Name'></input>
                <input type='button' onClick={this.handleSearch} value='Search'></input>
            </div>
            </>
        );
    }

}

export default Search;