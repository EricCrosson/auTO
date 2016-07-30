class MatchTable extends React.Component {
  constructor() {
    super();
    this.state = {}
  }

  render() {
    var rows = [];
    this.props.matches.forEach(function(match) {
      rows.push(<MatchRow bracketPosition={match.bracketPosition} player1={match.player1} player2={match.player2} setup={match.setup} key={match.bracketPosition} />); 
    });
    return (
      <div>
        <table>
          <thead>
            <tr>
              <th>Match</th>
              <th>Player 1</th>
              <th></th>
              <th>Player 2</th>
              <th></th>
              <th>Setup</th>
            </tr>
          </thead>
          <tbody>
            { rows }
          </tbody>
        </table>
      </div>
    );
  }
}

class MatchRow extends React.Component {
  constructor() {
    super();
    this.state = {
      data: {}
    }
  }

  render() {
    return (
      <tr>
        <td>{ this.props.bracketPosition }</td>
        <td>{ this.props.player1 }</td>
        <td> <input placeholder="Enter result"/> </td>
        <td>{ this.props.player2 }</td>
        <td> <input placeholder="Enter result"/> </td>
        <td>{ this.props.setup }</td>
        <td><button>Submit</button></td>
      </tr>
    );
  }
}


var MATCHES = [
  {bracketPosition: 'W1', player1: 'DTMP', player2: 'Zaxtorp', setup: '2'},
  {bracketPosition: 'WF', player1: 'Tirno', player2: 'Zaxtorp', setup: '1'},
];

ReactDOM.render(
  <MatchTable matches={MATCHES} />,
  document.getElementById('content')
);