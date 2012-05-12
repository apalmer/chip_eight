using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NUnit.Framework;

namespace Playground.Tests.DataAccess.ADOdotNET.EmployeeSearch
{
    [TestFixture]
    public class SearchTestFixture
    {
        [Test]
        public void SmokeTest()
        {
            var searchResults = Playground.DataAccess.ADOdotNET.EmployeeSearch.Search(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null);
        }
    }
}
