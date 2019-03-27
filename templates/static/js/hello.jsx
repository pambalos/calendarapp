

var realPython = React.createClass({
  render: function() {
    return(<h2> Hi From Real Python Class </h2>)
  }
});

ReactDOM.render(
  React.createElement(realPython, null),
  document.getElementById('content')
);
