class MatchTable extends React.Component {
  constructor() {
    super();
    this.state = {}
  }

  render() {
    var rows = [];
    var i = 1;
    var setup = '';

    this.props.matches.forEach(function(match) {
      if (i < 7) {
        setup = i;
        i++;
      }
      else {
        setup = ''; 
      }
      
      rows.push(<MatchRow bracketPosition={match.bracket_position} player1={match.player1[0]} player2={match.player2[0]} setup={setup} key={match.match_id} />); 
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
  }

  render() {
    var button;
    if (this.props.setup) {
      button = <td><button>Submit</button></td>
    }
    
    return (
      <tr>
        <td>{ this.props.bracketPosition }</td>
        <td>{ this.props.player1 }</td>
        <td> <input placeholder="Enter result"/> </td>
        <td>{ this.props.player2 }</td>
        <td> <input placeholder="Enter result"/> </td>
        <td>{ this.props.setup }</td>
        { button }
      </tr>
    );
  }
}


//var MATCHES = [
//  {bracketPosition: 'W1', player1: 'DTMP', player2: 'Zaxtorp', setup: '2'},
//  {bracketPosition: 'WF', player1: 'Tirno', player2: 'Zaxtorp', setup: '1'},
//];

var MATCHES = [];
$.get('/matches', function( data ){
  MATCHES = data['matches'];
  console.log(MATCHES);

  ReactDOM.render(
    <MatchTable matches={MATCHES} />,
    document.getElementById('content')
  );
});
