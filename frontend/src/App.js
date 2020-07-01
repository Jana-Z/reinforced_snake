import React from 'react';

function Square(props) {
  let backgroundColor = null; 
  switch (props.value){
    case (1):
      backgroundColor = 'red';
      break;
    case (2):
      case(3):
        backgroundColor = 'green';
        break;
    case (4):
      backgroundColor = 'black';
      break;
    default: backgroundColor = '#fff';
    break;
  }
  return (
    <button style = {{
      backgroundColor: backgroundColor,
      border: '1px solid #999',
      float: 'left',
      // fontSize: '24px',
      lineHeight: '34px',
      height: '34px',
      marginRight: '-1px',
      marginTop: '-1px',
      padding: 0,
      width: '34px',
    }} onClick={() => props.onClick(props.index)}/>
  );
}

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      obstacles: [],
      board : [0, 0, 0, 0, 0,
      3, 3, 0, 0, 0,
      2, 3, 0, 0, 0,
      0, 3, 0, 0, 0,
      0, 0, 1, 0, 0,]
    }
    this.renderSquare = this.renderSquare.bind(this);
    this.addObstacle = this.addObstacle.bind(this);
  }

  addObstacle(i){
    console.log(i)
    this.setState(state => {
      let new_board = [...state.board];
      new_board[i] = 4
      return{
      board: new_board
    }})
  }
  
  renderSquare(i) {
    console.log(i)
    return (
      <Square

        // onClick={() => this.props.onClick(i)}
        value = {this.state.board[i]}
        index = {i}
        onClick = {this.addObstacle}

      />
    )
    }

  render() {
    const row_style = {
      clear: "both",
      content: "",
      display: "table",
      // backgroundColor: 'blue',
      // width: '100%'
    };
    const grid_style = {
      // display: "flex",
      // flexDirection: "row"
    }
    return (
      <div style = {grid_style}>
        {this.state.obstacles}
        <div style={row_style}>
          {[...Array(5).keys()].map(i => this.renderSquare(i))}
        </div>
        <div style={row_style}>
        {[...Array(5).keys()].map(i => this.renderSquare(i+5))}
        </div>
        <div style={row_style}>
        {[...Array(5).keys()].map(i => this.renderSquare(i+10))}
        </div>
        <div style={row_style}>
        {[...Array(5).keys()].map(i => this.renderSquare(i+15))}
        </div>
        <div style={row_style}>
        {[...Array(5).keys()].map(i => this.renderSquare(i+20))}
        </div>
      </div>
    );
  }
}

export default App;
