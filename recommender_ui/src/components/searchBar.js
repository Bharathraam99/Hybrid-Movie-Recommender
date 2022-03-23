import React, { useState, useEffect, useRef } from "react";
import { TextField } from "@material-ui/core";
import Autocomplete, {
  createFilterOptions,
} from "@material-ui/lab/Autocomplete";
import Axios from "axios";
import ScaleLoader from "react-spinners/ScaleLoader";

const SearchBar = () => {
  const [myOptions, setMyOptions] = useState([]);
  const [moviesList, setMoviesList] = useState([]);
  const [recMovies, setRecMovies] = useState([]);
  const [twitterId, setTwitterId] = useState("");
  const [genre, setGenre] = useState([]);
  const [loading, setLoading] = useState(false);

  const valueRef = useRef("");
  const twitterIdRef = useRef("");

  const sendValue = () => {
    setLoading(true);
    setRecMovies(() => []);
    setGenre(() => []);
    let payload = { selectedMovies: moviesList, twitterId: twitterId };
    console.log("payload => ", payload);
    Axios.post("http://localhost:5000/getrec", payload).then((Response) => {
      setRecMovies([...Response.data.moviesList]);
      setGenre([...Response.data.predictedGenre]);
      setLoading(false);
      console.log(Response.data);
    });
    // console.log(recMovies);
  };

  const addMovie = (movie) => {
    let tempArr1 = moviesList;
    tempArr1.push(movie);
    setMoviesList([...tempArr1]);
    console.log(moviesList);
  };

  const clearSelection = () => {
    setMoviesList([]);
    setRecMovies([]);
    setTwitterId("");
    setGenre([]);
    console.log(moviesList);
  };

  useEffect(() => {
    let tempArr = [];
    fetch("http://localhost:5000/list")
      .then((Response) => Response.json())
      .then((res) => {
        res.map(function (movie) {
          return tempArr.push(movie.title);
        });
      });
    setMyOptions(tempArr);
    console.log(setMyOptions);
  }, []);

  const getDataFromAPI = () => {
    setMyOptions(myOptions);
  };

  const filterOptions = createFilterOptions({
    matchFrom: "any",
    limit: 500,
  });

  return (
    <div>
      <div className="centerBox">
        <div className="searchBarBox">
          <div className="container">
            <div className="row">
              <div className="col">
                <h4 id="enter_label">Enter your favorite films</h4>
                <Autocomplete
                  style={{ width: 300 }}
                  freeSolo
                  filterOptions={filterOptions}
                  autoComplete
                  autoHighlight
                  options={myOptions}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      onChange={getDataFromAPI}
                      variant="outlined"
                      label="Search Box"
                      inputRef={valueRef}
                      className="searchBar"
                    />
                  )}
                />
              </div>
              <div className="d-flex">
                {moviesList.map((movie, index) => (
                  <p key={index} id="movie_box">
                    {movie}
                  </p>
                ))}
              </div>
            </div>
            <button
              onClick={() => {
                addMovie(valueRef.current.value.split("(")[0].trim());
              }}
              id="addButton"
              className="btn btn-primary btn-lg"
            >
              Add
            </button>
            <button
              onClick={clearSelection}
              id="clearButton"
              className="btn btn-danger btn-lg"
            >
              Clear
            </button>
          </div>
          <div className="container">
            <input
              type="text"
              inputRef={twitterIdRef}
              value={twitterId}
              onChange={(e) => setTwitterId(e.target.value)}
              id="tidBox"
              placeholder="Twitter ID"
              className="mr-2"
            />
            <button
              onClick={sendValue}
              id="sendButton"
              className="btn btn-warning btn-lg"
              type="submit"
            >
              Generate
            </button>
          </div>
          <center>
            <ScaleLoader
              color="#36D7B7"
              loading={loading}
              height={50}
              width={8}
              radius={4}
              margin={4}
            />
          </center>
          <div className="container">
            <div className="row">
              {genre.map((genre, index) => (
                <p key={index} id="genre_box">
                  {genre}
                </p>
              ))}
            </div>
          </div>

          <div className="container">
            <div className="row">
              {recMovies.map((movie, index) => (
                <p key={index} id="rec_movie_box">
                  {movie}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
