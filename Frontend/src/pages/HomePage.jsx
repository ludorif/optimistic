import React from 'react'
import '../App.css'
import axios from "axios";
import HistoryPart from '../components/HistoryPart.jsx';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.updateInput = this.updateInput.bind(this);
        this.state = {
            title: 'Hello world!',
            content: 'content!',
            url: 'https://www.pexels.com/photo/book-with-along-16700988/',
            username : ''
        }
    }

    updateInput(event) {
        this.setState({
            username: event.target.value
        })
    }


    handleTextChange = () => {
        axios.post('events/?story='+this.state.username)
            .then(response => {

                const obj = JSON.parse(response.data);

                this.setState({
                    title: obj.title,
                    content: obj.content,
                    url: `https://images.pexels.com/photos/${obj.photoId}/pexels-photo-${obj.photoId}.jpeg`
                })
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }






    render() {


        return (
            <div>
                <h2>{this.state.title}</h2>
                <p>{this.state.content} </p>
                <img width={500} height={500} src={this.state.url}/>
                <input  onChange={this.updateInput}/>
                <button onClick={this.handleTextChange}>Change text</button>


            </div>
        )
    }
}

export default App
