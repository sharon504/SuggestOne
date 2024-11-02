
import { Button } from "@mui/material"
export default function Searched({ heading, description }) {
    return( 
 
    <motion.div
      className="flex flex-col border border-purple-500 space-y-4 mt-6 z-50
       mx-auto p-4 bg-gray-900 rounded-lg shadow-lg transition-all overflow-hidden-all duration-300 ease-in-out hover:scale-105 "
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-2xl font-semibold text-left text-purple-300">{heading}</h2>
      <p className="text-left text-gray-400 mb-5 ">{description}</p>
      <Button variant="outline" className="w-full bg-purple-700 text-white ">
        More Info
      </Button>
    </motion.div>
  )
}