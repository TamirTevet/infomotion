import React from 'react';
import logo from './logo.svg';
import './App.css';

import Searchbar from './components/searchbar/Searchbar';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
// import Logo from './components/logo/Logo';
class App extends React.Component {
  state = {
    data: [],
  }
  submitWordHandler(e) {
    e.preventDefault();
    const word = e.target.elements.word.value;
    fetch('http://localhost:3000/words?word=' + word)
      .then(res => res.json())
      .then(data => {
        if (data.length === 0) {
          alert('There are no results');
        } else {
          this.setState({ data: data })
        }
      })
      .catch(e => console.error(e));
  }

  render() {
    const classes = makeStyles({
      table: {
        minWidth: 650,
      },
      m: {
        margin: '0 auto',
      }
    });

    const isDataEmpty = this.state.data.length == 0;
    return (
      <div className="App">
        {/* <Logo name='InfoMotion' /> */}
        <Searchbar name='word' onSubmit={(e) => this.submitWordHandler(e)} />
        {isDataEmpty ? null : (
          <div className={classes.m}>
            <TableContainer component={Paper}>
              <Table className={classes.table} aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell>Id</TableCell>
                    <TableCell align="center">Name</TableCell>
                    <TableCell align="center">Video Name</TableCell>
                    <TableCell align="center">Part</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {this.state.data.map((row) => (
                    <TableRow key={row._id}>
                      <TableCell component="th" scope="row">{row._id}</TableCell>
                      <TableCell align="center">{row.name}</TableCell>
                      <TableCell align="center">{row.stream_name}</TableCell>
                      <TableCell align="center">{row.part}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </div>
        )}
      </div>
    )
  };
}

export default App;
