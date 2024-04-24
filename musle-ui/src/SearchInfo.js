import React from "react";

class SearchInfo extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            genres: this.props.genres,
            artistID: this.props.artistID,
            popularNames: []
        }
    }

    fetchSongs = () => {
        fetch(`http://127.0.0.1:5000/songs?popular=${this.props.artistID}`, {

        }).then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            return 'No popular songs found...'
        }
        }).then(jString => {
        const names = [];
        const jData = JSON.parse(jString);
        jData.map(obj => names.push(obj.name));
        this.setState({popularNames: names})
        })
    }

    componentDidMount() {
        this.fetchSongs();
    }

    componentDidUpdate(prevProps) {
        if (prevProps.artistID !== this.props.artistID) {
            this.fetchSongs();
        }
    }

    render() {



        return (
            <>
            <div className="info-div">
                <p>{this.props.name}</p>

                <p>Popular Songs: {this.state.popularNames.join(', ')}</p>
                <p>Genres: {this.props.genres.map(g => {
                    const splitGenre = g.split(' ');
                    let formatted = splitGenre.map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
                    return formatted;
                }).join(', ')}</p>
            </div>
            </>
        );
    }


}

export default SearchInfo;