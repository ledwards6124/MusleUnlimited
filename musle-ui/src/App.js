import logo from './logo.svg';
import './App.css';
import Search from './Search';
import { useState } from 'react';
import SearchInfo from './SearchInfo';

function App() {

  const [searches, setSearches] = useState([]);

  const handleSearch = (searchJSON) => {
    setSearches(searchJSON);
  }

  return (
    <>
    <Search onSearch={handleSearch}></Search>
    {searches.map((s, index) => (
      <SearchInfo className='search-info' key={index} name={s.name} genres={s.genres} artistID={s.id}></SearchInfo>
    ))}
    </>
  );
}

export default App;
