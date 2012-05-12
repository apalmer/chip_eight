using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Playground.Controllers
{
    public class EmployeeSearchApiController : Controller
    {
        //
        // GET: /EmployeeSearchApi/

        public ActionResult Index(Playground.BusinessLogic.EmployeeSearchCriteria searchCriteria)
        {
            var json = new JsonResult();
            json.JsonRequestBehavior = JsonRequestBehavior.AllowGet;

            if (!searchCriteria.Validate())
            {
                json.Data = searchCriteria.ValidationErrors;
            }
            else
            {

                var search = new Playground.BusinessLogic.EmployeeSearch();
                var results = search.Search(searchCriteria);
                json.Data = results;
            }
            return json;
        }

    }
}
