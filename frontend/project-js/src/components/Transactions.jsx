function Transactions() {
  return (
    <div className="table-responsive">
      <table className="table .table-hover table-bordered">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">points</th>
            <th scope="col">date</th>
            <th scope="col">question</th>
            <th scope="col">type</th>
          </tr>
        </thead>
        <tbody className="table-group-divider">
          <tr>
            <th scope="row">1</th>
            <td>1</td>
            <td>20/11/2023</td>
            <td>
              Lorem ipsum dolor, sit amet consectetur adipisicing elit. Iure,
              autem?
            </td>
            <td>earning</td>
          </tr>
          <tr>
            <th scope="row">2</th>
            <td>5</td>
            <td>20/11/2023</td>
            <td>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Totam,
              architecto!
            </td>
            <td>earning</td>
          </tr>
          <tr>
            <th scope="row">3</th>
            <td>2</td>
            <td>20/11/2023</td>
            <td>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Ut, sed.
            </td>
            <td>earning</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Transactions;
